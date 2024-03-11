import {
  registerDecorator,
  ValidationOptions,
  ValidatorConstraint,
  ValidatorConstraintInterface,
} from 'class-validator';
import { isCuid } from '@paralleldrive/cuid2';

@ValidatorConstraint({ async: true })
export class validateCUID implements ValidatorConstraintInterface {
  validate(userId: string) {
    return isCuid(userId);
  }

  defaultMessage(): string {
    return 'userId must be a CUID';
  }
}

export function IsCUID(validationOptions?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      target: object.constructor,
      propertyName: propertyName,
      options: validationOptions,
      constraints: [],
      validator: validateCUID,
    });
  };
}
